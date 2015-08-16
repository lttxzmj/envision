var gulp       = require('gulp'),
    stylus     = require('gulp-stylus'),
    browserify = require('browserify'),
    del        = require('del'),
    nib        = require('nib');

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
  },
  watching: {
    stylesheets: 'f2e/css/**.styl',
    scripts: 'f2e/js/**.js',
  }
};

gulp.task('build', ['build:scripts', 'build:stylesheets']);

gulp.task('build:scripts', function() {

});

gulp.task('build:stylesheets', function() {
  gulp.src(paths.source.stylesheets)
      .pipe(stylus({
        compress: true,
        use: nib()
      }))
      .pipe(gulp.dest(paths.target.stylesheets))
});

gulp.task('watch', ['build'], function() {
  gulp.watch(paths.watching.scripts, ['build:scripts'])
  gulp.watch(paths.watching.stylesheets, ['build:stylesheets'])
})

gulp.task('clean', function(cb) {
  del([paths.target.root + '/*', '!.gitignore'], cb)
})
