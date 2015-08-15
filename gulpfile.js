var gulp       = require('gulp'),
    stylus     = require('gulp-stylus'),
    browserify = require('browserify'),
    del        = require('del');

var paths = {
  source: {
    stylesheets: [
      'f2e/css/base.styl'
    ],
    scripts: [
    ]
  },
  target: {
    stylesheets: 'envision/static/css',
    scripts: 'envision/static/js',
    root: 'envision/static'
  }
};

gulp.task('build', ['build:scripts', 'build:stylesheets']);

gulp.task('build:scripts', function() {

});

gulp.task('build:stylesheets', function() {
  gulp.src(paths.source.stylesheets)
      .pipe(stylus({
        compress: true,
      }))
      .pipe(gulp.dest(paths.target.stylesheets))
});

gulp.task('watch', ['build'], function() {
  gulp.watch(paths.source.scripts, ['build:scripts'])
  gulp.watch(paths.source.stylesheets, ['build:stylesheets'])
})

gulp.task('clean', function(cb) {
  del([paths.target.root + '/*', '!.gitignore'], cb)
})
