//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    img: '',
    imgFile: '',
    generate: '',
    block: 'none',
    style: 1,
    style_pos: [220, 5],
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
      sizeType: ['compressed'],
      sourceType: ['album', 'camera'],
      success: function (res) {
        let base64 = wx.getFileSystemManager().readFileSync(res.tempFilePaths[0], 'base64')
        // console.log(base64)

        that.setData({
          imgFile: res.tempFilePaths[0],
          img: base64,
          generate: ''
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
  },

  uploadImage: function (e) {
    console.log('transfer')

    var that = this

    this.setData({
      block: 'block'
    })

    wx.showToast({
      title: '由于个人服务器资源有限\n请稍等几秒返回计算结果',
      icon: 'none',
      duration: 3000
    })

    wx.uploadFile({
      url: 'https://www.bugstop.site/nst/',
      filePath: that.data.imgFile,
      name: 'file',
      formData: {
        'style': that.data.style,
        'img': that.data.img
      },
      success(res) {
        const data = res.data
        var obj = JSON.parse(data);

        that.setData({
          generate: obj.rc,
          block: 'none'
        })
        
        console.log(obj.rc)
        console.log('done')
      }
    })
  },
})
