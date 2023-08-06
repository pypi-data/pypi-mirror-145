Blockly.Python.pins = function() {
    var code = this.getFieldValue('PIN');
    return [code, Blockly.Python.ORDER_ATOMIC];
  };

Blockly.Python.inout_highlow = function () {
    // Boolean values HIGH and LOW.
    var code = (this.getFieldValue('BOOL') == 'HIGH') ? 'HIGH' : 'LOW';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Python['GPIO_model'] = function () {
    Blockly.Python.definitions_['GPIO'] = 'import RPi.GPIO as GPIO';
    var model = this.getFieldValue('MODEL')
    var code = 'GPIO.setmode(GPIO.'+ model + ')\n';
    return code;
};

Blockly.Python['GPIO_getmode'] = function () {
    Blockly.Python.definitions_['GPIO'] = 'import RPi.GPIO as GPIO';
    Blockly.Python.definitions_['var_declare_'+'NAME'] = 'sss';
    var code = 'GPIO.getmode()';
    return [code,Blockly.Python.ORDER_ATOMIC];
};

Blockly.Python['GPIO_setup'] = function () {
    Blockly.Python.definitions_['GPIO'] = 'import RPi.GPIO as GPIO';
    var pin =  Blockly.Python.valueToCode(this, 'PIN', Blockly.Python.ORDER_ATOMIC);
    var model = this.getFieldValue('MODEL');
    var code = 'GPIO.setup('+pin+', GPIO.'+model+')\n';
    return code;
};

Blockly.Python['GPIO_out'] = function () {
    Blockly.Python.definitions_['GPIO'] = 'import RPi.GPIO as GPIO';
    var pin =  Blockly.Python.valueToCode(this, 'PIN', Blockly.Python.ORDER_ATOMIC);
    var model = Blockly.Python.valueToCode(this, 'STAT', Blockly.Python.ORDER_ATOMIC);
    var code = 'GPIO.output('+pin+', GPIO.'+model+')\n';
    return code;
};

Blockly.Python['GPIO_in'] = function () {
    Blockly.Python.definitions_['GPIO'] = 'import RPi.GPIO as GPIO';
    var pin =  Blockly.Python.valueToCode(this, 'PIN', Blockly.Python.ORDER_ATOMIC);
    var code = 'GPIO.input('+pin+')\n';
    return [code,Blockly.Python.ORDER_ATOMIC];
};

Blockly.Python['GPIO_pwm_init'] = function () {
    Blockly.Python.definitions_['GPIO'] = 'import RPi.GPIO as GPIO';
    var pin =  Blockly.Python.valueToCode(this, 'PIN', Blockly.Python.ORDER_ATOMIC);
    var hz =  Blockly.Python.valueToCode(this, 'HZ', Blockly.Python.ORDER_ATOMIC);
    var code ='GPIO.PWM('+pin+', '+hz+') ';
    return [code,Blockly.Python.ORDER_ATOMIC];
};

Blockly.Python['GPIO_pwm_start'] = function () {
    Blockly.Python.definitions_['GPIO'] = 'import RPi.GPIO as GPIO';
    var pin =  Blockly.Python.valueToCode(this, 'PIN', Blockly.Python.ORDER_ATOMIC);
    var dc =  Blockly.Python.valueToCode(this, 'DC', Blockly.Python.ORDER_ATOMIC);
    var code =pin+'.start('+dc+')\n'
    return code;
};

Blockly.Python['GPIO_pwm_ChangeFrequency'] = function () {
    Blockly.Python.definitions_['GPIO'] = 'import RPi.GPIO as GPIO';
    var pin =  Blockly.Python.valueToCode(this, 'PIN', Blockly.Python.ORDER_ATOMIC);
    var hz =  Blockly.Python.valueToCode(this, 'HZ', Blockly.Python.ORDER_ATOMIC);
    var code =pin+'.ChangeFrequency('+hz+')\n'
    return code;
};

Blockly.Python['GPIO_pwm_ChangeDutyCycle'] = function () {
    Blockly.Python.definitions_['GPIO'] = 'import RPi.GPIO as GPIO';
    var pin =  Blockly.Python.valueToCode(this, 'PIN', Blockly.Python.ORDER_ATOMIC);
    var dc =  Blockly.Python.valueToCode(this, 'DC', Blockly.Python.ORDER_ATOMIC);
    var code =pin+'.ChangeDutyCycle('+dc+')\n'
    return code;
};