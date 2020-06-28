//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    img: '',
    imgFile: '',
    generate: '',
    block: 'none',
    showimg: 'none',
    loss: 'none',
    style: 1,
    style_pos: [220, 5],
  },

  //事件处理函数
  bindViewTap: function () {
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
    var y = parseInt((id - 1) / 3)
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
    var that = this

    this.setData({
      block: 'block'
    })

    wx.showToast({
      title: '由于个人服务器资源有限\n请稍等几秒返回计算结果',
      icon: 'none',
      duration: 6000,
      mask: true,
    })

    console.log('transfer')

    wx.uploadFile({
      url: 'https://www.bugstop.site/nst/',
      filePath: that.data.imgFile,
      name: 'file',
      formData: {
        'style': that.data.style,
        'img': that.data.img
      },
      success(res) {
        try {
          const data = res.data
          var obj = JSON.parse(data);

          that.setData({
            generate: obj.rc,
          })

          console.log(obj)
          console.log(obj.rc)

        } catch (e) {
          console.log(e)

          that.setData({
            img: '',
            imgFile: '',
            generate: '',
          })

          wx.showToast({
            title: '远程服务器异常',
            icon: 'none',
            duration: 1000,
          })
        }
      },

      fail(res) {
        console.log(res)
      },

      complete(res) {
        that.setData({
          block: 'none'
        })
        console.log('done')
      }
    })
  },

  showImage: function () {
    console.log("show")
    this.setData({
      showimg: 'block'
    })
  },

  hideImage: function () {
    console.log("hide")
    this.setData({
      showimg: 'none'
    })
  },

  hideLoss: function () {
    this.setData({
      showimg: 'block',
      loss: 'none'
    })
  },

  downImage: function () {
    console.log("down")
    var that = this

    wx.showActionSheet({
			itemList: ['查看训练Loss曲线', '保持图片到本地'],
			success: function(res) {
        console.log(res.tapIndex)
        
        if (res.tapIndex == 0) {
          that.setData({
            loss: 'block',
            showimg: 'none'
          })
        }

        if (res.tapIndex == 1) {
          var timestamp = new Date().getTime();
          var aa = wx.getFileSystemManager();
          aa.writeFile({
            filePath: wx.env.USER_DATA_PATH + '/' + timestamp + '.png',
            data: that.data.generate,
            encoding: 'base64',
            success: res => {
              wx.saveImageToPhotosAlbum({
                filePath: wx.env.USER_DATA_PATH + '/' + timestamp + '.png',
                success: function (res) {
                  wx.showToast({
                    title: '保存成功',
                  })
                },
                fail: function (err) {
                  console.log(err)
                }
              })
              console.log(res)
            },
            fail: err => {
              console.log(err)
            }
          })
        }
			},
			fail: function(res) {
				console.log(res.errMsg)
			}
    })
    

    /*
    wx.showModal({
      title: '保存图片',
      content: '保存图片到系统相册',
      success(res) {
        if (res.confirm) {
          console.log('用户点击确定')

          var timestamp = new Date().getTime();
          var aa = wx.getFileSystemManager();
          aa.writeFile({
            filePath: wx.env.USER_DATA_PATH + '/' + timestamp + '.png',
            data: that.data.generate,
            encoding: 'base64',
            success: res => {
              wx.saveImageToPhotosAlbum({
                filePath: wx.env.USER_DATA_PATH + '/' + timestamp + '.png',
                success: function (res) {
                  wx.showToast({
                    title: '保存成功',
                  })
                },
                fail: function (err) {
                  console.log(err)
                }
              })
              console.log(res)
            },
            fail: err => {
              console.log(err)
            }
          })
        } else if (res.cancel) {
          console.log('用户点击取消')
        }
      }
    })
    */
  }
})