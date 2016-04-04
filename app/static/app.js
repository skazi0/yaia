var YaiaApp = angular.module('YaiaApp', ['ngRoute']);

YaiaApp.config(function ($routeProvider) {
  $routeProvider
    .when('/', {templateUrl: 'static/partials/home.html'});
});