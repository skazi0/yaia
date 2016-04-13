'use strict';

var YaiaApp = angular.module('YaiaApp', ['ui.router', 'yaia.home', 'yaia.login', 'yaia.invoices', 'yaia.welcome', 'restangular', 'yaia.auth']);

YaiaApp.config(['$stateProvider', '$urlRouterProvider', 'RestangularProvider', function ($stateProvider, $urlRouterProvider, RestangularProvider) {
  RestangularProvider.setBaseUrl('api');
  $urlRouterProvider.otherwise('/welcome');
  $stateProvider
    .state('anon', {abstract: true, templateUrl: 'static/views/anon.html', data: {access: 'anon'}})
    .state('user', {abstract: true, templateUrl: 'static/views/user.html', controller: 'UserCtrl', data: {access: 'user'}});
}]);

YaiaApp.controller('UserCtrl', ['$scope', '$state', 'Auth', function($scope, $state, Auth) {
    $scope.current_user = Auth.currentUser();

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

YaiaApp.run(['$rootScope', '$state', 'Auth', function($rootScope, $state, Auth) {
    // fetch initial auth info from server
    console.log('init auth info');
    Auth.refresh();

    $rootScope.$on('$stateChangeSuccess', function(event, toState, toParams, fromState, fromParams) {
        if (!Auth.isAuthorized(toState.data.access)) {
            $state.transitionTo('anon.login');
        }
    });
}]);