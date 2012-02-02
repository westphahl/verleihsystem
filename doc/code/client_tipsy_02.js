$(function() {
    $('*[rel=tipsy_n]').tipsy({delayIn: 500, gravity: 'n'});
    $('*[rel=tipsy_w]').tipsy({fade: true, gravity: 'w'});
    $('*[rel=tipsy_s]').tipsy({delayIn: 500, gravity: 's'});
    $('*[rel=tipsy_e]').tipsy({fade: true, gravity: 'e'});
    $('*[rel=tipsy_adminopt]').tipsy({delayIn: 500, fade: true, gravity: 'n'});
});
