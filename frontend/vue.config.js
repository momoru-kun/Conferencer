module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  pages: {
    index: {
      entry: 'index/main.js',
      template: 'public/index.html',
      filename: process.env.NODE_ENV === 'production' ? '../../templates/index.html' : 'index.html',
      title: 'Conferencer',
      chunks: ['chunk-vendors', 'chunk-common', 'index']
    },
    quiz: {
      entry: 'quiz/main.js',
      template: 'public/quiz.html',
      filename: '../../templates/quiz.html',
      title: 'Запись на конференцию',
      chunks: ['chunk-vendors', 'chunk-common', 'quiz']
    },
    admin: {
      entry: 'admin/main.js',
      template: 'public/admin.html',
      filename: process.env.NODE_ENV === 'production' ? '../../templates/admin.html' : 'admin.html',
      title: 'Управление конференциями',
      chunks: ['chunk-vendors', 'chunk-common', 'admin']
    }
  },
  outputDir: process.env.NODE_ENV === 'production' ? '../client/static' : 'dist/',
  indexPath: process.env.NODE_ENV === 'production' ? '../../templates/index.html' : 'index.html',
  assetsDir: '',
  publicPath: process.env.NODE_ENV === 'production' ? 'static' : '/',
  
  devServer: {
    proxy: {
      '^/api': {
        target: 'http://localhost:8000/'
      }
    }
  }
}
