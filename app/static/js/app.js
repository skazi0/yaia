'use strict';

var YaiaApp = angular.module('YaiaApp', ['ui.router', 'yaia.home', 'yaia.login', 'yaia.invoices', 'yaia.welcome', 'restangular', 'yaia.auth']);

YaiaApp.config(['$stateProvider', '$urlRouterProvider', 'RestangularProvider', function ($stateProvider, $urlRouterProvider, RestangularProvider) {
  RestangularProvider.setBaseUrl('api');
  $urlRouterProvider.otherwise('/welcome');
  $stateProvider
    .state('anon', {abstract: true, templateUrl: 'static/views/anon.html'})
    .state('user', {abstract: true, templateUrl: 'static/views/user.html', controller: 'UserCtrl'});
}]);

YaiaApp.controller('UserCtrl', ['$scope', '$state', 'Auth', function($scope, $state, Auth) {
    $scope.$on('authChanged', function(event, authInfo) { 
        $scope.current_user = authInfo;
        console.log('auth info received' + authInfo);
    });

    $scope.logout = function() {
        Auth.logout().then(
            function() {
                $state.transitionTo('anon.welcome');
             }
        );
    };
}]);
