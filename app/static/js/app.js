'use strict';

var YaiaApp = angular.module('YaiaApp', ['ngRoute', 'yaia.home', 'yaia.login', 'yaia.invoices']);

YaiaApp.config(['$routeProvider', function ($routeProvider) {
  $routeProvider
    .otherwise({redirectTo: '/home'});
}]);
