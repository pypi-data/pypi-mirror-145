Blockly.Python.baiduAI_init=function(a){
    Blockly.Python.definitions_['MxbaiduAi_init'] = 'from Mx import image';
    var app_id = Blockly.Python.valueToCode(this,'APP_ID',Blockly.Python.ORDER_ASSIGNMENT);
    var api_key = Blockly.Python.valueToCode(this,'API_KEY',Blockly.Python.ORDER_ASSIGNMENT);
    var api_sckey = Blockly.Python.valueToCode(this,'API_SCKEY',Blockly.Python.ORDER_ASSIGNMENT);
    var code= 'image.imageAI('+app_id+','+api_key+','+api_sckey+')';
    return [code,Blockly.Python.ORDER_ATOMIC];
}

Blockly.Python.baiduAI_image=function(a){
    var v = Blockly.Python.valueToCode(this,'V',Blockly.Python.ORDER_ASSIGNMENT);
    var img = Blockly.Python.valueToCode(this,'IMG',Blockly.Python.ORDER_ASSIGNMENT);
    var model = this.getFieldValue('MOEDL')
    var code= v+'.'+model+'('+img+');'
    return code;
}

Blockly.Python.baiduAI_result=function(a){
    var v = Blockly.Python.valueToCode(this,'V',Blockly.Python.ORDER_ASSIGNMENT);
    var code = v+'.result()'
    return [code,Blockly.Python.ORDER_ATOMIC];
}

