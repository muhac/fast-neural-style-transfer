//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    motto: 'Hello World',
    imgFile: '',
    style: 1,
    style_pos: [220, 5]
  },

  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },

  onLoad: function () {
    this.setData({
      //imgFile: 123,
    })
    console.log('start')
  },

  chooseImage: function () {
    var that = this;
    wx.chooseImage({
      count: 1,
      sizeType: ['original', 'compressed'],
      sourceType: ['album', 'camera'],
      success(res) {
        console.log(res)
        // tempFilePath可以作为img标签的src属性显示图片
        that.setData({
          imgFile: res.tempFilePaths[0]
        })
      }
    })
  },

  chooseStyle: function (e) {
    var id = e.currentTarget.dataset['index']
    var y = parseInt((id-1) / 3)
    var x = parseInt(id - 1 - y * 3)
    this.setData({
      style: id,
      style_pos: [220 + 204 * x, 5 + 204 * y]
    })
  },

  deleteImage: function () {
    this.setData({
      imgFile: ''
    })
  }
})

