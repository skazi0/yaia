'use strict';

var YaiaApp = angular.module('YaiaApp', ['ui.router', 'yaia.home', 'yaia.login', 'yaia.invoices']);

YaiaApp.config(['$stateProvider', '$urlRouterProvider', function ($stateProvider, $urlRouterProvider) {
  $urlRouterProvider.otherwise('/home');
}]);
