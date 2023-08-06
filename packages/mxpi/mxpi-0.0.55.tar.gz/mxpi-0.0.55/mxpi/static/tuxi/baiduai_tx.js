Blockly.Blocks.baiduAI_init= {
    init: function() {
    this.appendDummyInput()
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("初始化百度AI");
    this.appendValueInput("APP_ID")
        .setCheck(String)
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(" APP_ID");
    this.appendValueInput("API_KEY")
        .setCheck(String)
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(" APIKey");
    this.appendValueInput("API_SCKEY")
        .setCheck(String)
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField(" SecretKey");
    this.setInputsInline(false);
    this.setOutput(true, null);
    this.setStyle('BaiduAI_blocks');
    this.setTooltip("初始化百度AI");
    this.setHelpUrl("");
    }
  };
  
  Blockly.Blocks.baiduAI_image= {
    init: function() {
    this.appendDummyInput()
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("调用");
    this.appendValueInput("V")
        .setCheck(null)
        .setAlign(Blockly.ALIGN_RIGHT);
    this.appendValueInput("IMG")
        .setCheck(String)
        .appendField("对图片");
    this.appendDummyInput()
        .setAlign(Blockly.ALIGN_RIGHT)
        .appendField("进行")
        .appendField(new Blockly.FieldDropdown([["通用场景识别","advancedGeneral"],["图像主题检测","objectDetect"],["菜品识别","dishDetect"],["商标识别","logoSearch"],["动物识别","animalDetect"],["植物识别","plantDetect"],["地标识别","landmark"],["果蔬识别","ingredient"],["货币识别","currency"],["车辆识别","carDetect"]]), "MOEDL");
    this.setInputsInline(true);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setStyle('BaiduAI_blocks');
    this.setTooltip("进行百度AI识别");
    this.setHelpUrl("");
    }
  };

  Blockly.Blocks.baiduAI_result= {
    init: function() {
    this.appendDummyInput()
        .appendField("获取");
    this.appendValueInput("V")
        .setCheck(null);
    this.appendDummyInput()
        .appendField("识别结果");
    this.setInputsInline(true);
    this.setOutput(true, null);
    this.setStyle('BaiduAI_blocks');
    this.setTooltip("获取图像识别结果");
    this.setHelpUrl("");
    }
  };