from string import Template

from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Image, \
    Spacer, TableStyle, ParagraphAndImage
from django.core.exceptions import ObjectDoesNotExist


class DummyProfile(object):
    """
    Dummy profile if a user has no assigned profile.
    """
    student_number = None
    phone = None
    mobile_phone = None 


class BorrowFormTemplate(SimpleDocTemplate):
    """
    Template for a PDF borrow form.
    """

    title = u"Leihschein"
    hint = u"""<i>Hinweis:</i> Der Leihschein muss in <b>zweifacher
    Ausf\u00fchrung</b> ausgedruckt und mitgebracht werden. Andernfalls
    k\u00f6nnen die reservierten Produkte leider nicht ausgeliehen werden!
    """
    reservation_template = Template("""
    <b>Leihzeitraum: ${start_date} bis ${end_date}</b><br/>
    <b>Kommentar:</b> ${comments}
    """)
    student_template = Template(u"""
    <b>Name:</b> ${name} ${surname}<br/>
    <b>Matrikelnr.:</b> ${student_id}<br/>
    <b>Telefon:</b> ${phone}<br/>
    <b>Mobil:</b> ${mobil}<br/>
    <b>Email:</b> ${email}
    """)
    blank_line = "______________________________"
    reservation_data = []
    flowables = []
    logo = None

    def __init__(self, path, reservation):
        """
        Initialize a new PDF form.

        The path argument must be the absolute path for the resulting
        destination file. The reservation argument specifies the reservation
        the form is created for.
        """
        SimpleDocTemplate.__init__(self, path)
        # Get a default stylesheet
        self.styles = getSampleStyleSheet()
        self._set_data(reservation)

    def set_logo(self, logo, width, height):
        """
        Set a optional logo for display in the output file.
        """
        self.logo = logo
        self.logo_width = width
        self.logo_height = height

    def _set_data(self, reservation):
        """
        Internal method for setting and formatting the reservation data.
        """
        self.start_date = reservation.start_date.strftime('%d.%m.%Y')
        self.end_date = reservation.end_date.strftime('%d.%m.%Y')
        self.comments = reservation.comments if reservation.comments else "--"
        self.student = reservation.user
        self.reservationentries = reservation.reservationentry_set.all()

    def _get_head(self):
        """
        Internal method for creating and returning the flowables for the
        head section of the document.
        """
        title = Paragraph(u"Leihschein", self.styles['h1'])
        if self.logo and self.logo_width and self.logo_height:
            img = Image(self.logo, self.logo_width*mm, self.logo_height*mm)
            img.hAlign = 'RIGHT'
            return ParagraphAndImage(title, img)
        else:
            return title

    def _get_hint(self):
        """
        Internal method for creating and formatting the hint flowable.
        """
        text = Paragraph(self.hint, self.styles['Normal'])
        column_widths = [160*mm]
        tstyle = TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ])
        return Table([[text]], colWidths=column_widths, style=tstyle)

    def _get_student_data(self):
        """
        Internal method for creating and formatting the student data flowables.

        Uses a dummy profile if the user has no 'real' profile.
        """
        try:
            profile = self.student.get_profile()
        except ObjectDoesNotExist:
            profile = DummyProfile()
        student_id = profile.student_number or self.blank_line
        phone = profile.phone or self.blank_line
        mobil = profile.mobile_phone or self.blank_line

        return Paragraph(self.student_template.substitute(
            name=self.student.first_name, surname=self.student.last_name,
            student_id=student_id, phone=phone,
            mobil=mobil, email=self.student.email), self.styles['Normal'])

    def _get_reservation_data(self):
        """
        Internal mehtod for creating and formatting the flowables for the
        reservation data.
        """
        return Paragraph(self.reservation_template.substitute(
            start_date=self.start_date, end_date=self.end_date,
            comments=self.comments), self.styles['Normal'])

    def _get_table_titles(self):
        """
        Internal method for creating and formatting the title flowables for the
        table of reserved products.
        """
        return [
            [Paragraph(u"<b>Titel/Beschreibung</b>", self.styles['Normal']),
                Paragraph(u"<b>Anmerkung</b>", self.styles['Normal']),
                Paragraph(u"<b>S/N</b>", self.styles['Normal']),
            ],
        ]

    def _get_reservation_table(self):
        """
        Internal method for creating and formatting the flowables for the
        table of reserved products.
        """
        reservation_table = []
        for entry in self.reservationentries:
            reservation_table.append([
                Paragraph(entry.product.product_type.name,
                    self.styles['Normal']),
                Paragraph(entry.product.brief_description,
                    self.styles['Normal']),
                Paragraph(entry.product.sn, self.styles['Normal'])])
        table = self._get_table_titles() + reservation_table
        column_widths = [40*mm, 80*mm, 40*mm]
        tstyle = TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
        ])
        return Table(table, colWidths=column_widths,
            repeatRows=1, style=tstyle)

    def _get_signature_line(self):
        """
        Internal method for creating and formatting the flowables for the
        signature line.
        """
        column_widths = [70*mm, 20*mm, 70*mm]
        tstyle = TableStyle([
            ('LINEBELOW', (0, 0), (0, 0), 0.5, colors.black),
            ('LINEBELOW', (2, 0), (2, 0), 0.5, colors.black),
            ('ALIGN', (0, 1), (-1, 1), 'RIGHT'),
        ])
        signature_data = [
            [self.start_date, "", self.end_date],
            [u"Unterschrift (Ausleihe)", "", u"Unterschrift (R\u00fcckgabe)"]
        ]
        return Table(signature_data, colWidths=column_widths,
            repeatRows=1, style=tstyle)

    def build(self):
        """
        Build function for collecting all the needed flowables, combining
        them and creating the PDF file.
        """
        # Collect and combine the flowables
        flowables = [self._get_head()]
        flowables.append(Spacer(1, 10*mm))
        flowables.append(self._get_hint())
        flowables.append(Spacer(1, 10*mm))
        flowables.append(self._get_student_data())
        flowables.append(Spacer(1, 5*mm))
        flowables.append(self._get_reservation_data())
        flowables.append(Spacer(1, 10*mm))
        flowables.append(self._get_reservation_table())
        flowables.append(Spacer(1, 20*mm))
        flowables.append(self._get_signature_line())
        # Build the document
        SimpleDocTemplate.build(self, flowables)
