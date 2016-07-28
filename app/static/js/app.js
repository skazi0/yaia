'use strict';

var YaiaApp = angular.module('YaiaApp', ['ui.router', 'ui.router.title', 'ui.gravatar', 'yaia.home', 'yaia.login', 'yaia.invoices', 'yaia.welcome', 'restangular', 'yaia.auth', 'yaia.customers', 'yaia.profile']);

YaiaApp.config(['$stateProvider', '$urlRouterProvider', 'RestangularProvider', function ($stateProvider, $urlRouterProvider, RestangularProvider) {
  RestangularProvider.setBaseUrl('api');
  $urlRouterProvider.otherwise('/welcome');
  $stateProvider
    .state('anon', {abstract: true, templateUrl: 'static/views/partials/anon.html', data: {access: 'anon'}})
    .state('user', {abstract: true, templateUrl: 'static/views/partials/user.html', controller: 'UserCtrl', data: {access: 'user'}});
}]);

// based on https://docs.angularjs.org/error/ngModel/numfmt
YaiaApp.directive('stringToNumber', function() {
  return {
    require: 'ngModel',
    link: function(scope, element, attrs, ngModel) {
      ngModel.$parsers.push(function(value) {
        return value.toFixed(2);
      });
      ngModel.$formatters.push(function(value) {
        return parseFloat(value, 10);
      });
    }
  };
});

YaiaApp.controller('UserCtrl', ['$scope', '$state', 'Auth', function($scope, $state, Auth) {
    $scope.$state = $state;
    $scope.current_user = Auth.currentUser();

    $scope.$on('authChanged', function(event, authInfo) { 
        $scope.current_user = authInfo;
        console.log('auth info received' + authInfo);
    });

    $scope.logout = function() {
        Auth.logout().then(
            function() {
                $state.go('anon.welcome');
             }
        );
    };
}]);

YaiaApp.run(['$rootScope', '$state', 'Auth', function($rootScope, $state, Auth) {
    // fetch initial auth info from server
    console.log('init auth info');
    Auth.refresh();

    $rootScope.$on('$stateChangeSuccess', function(event, toState, toParams, fromState, fromParams) {
        // clear old targetState to avoid weird state changes when not using 'forced' login page immediately but switching between some other anon pages before logging in
        if (toState.name != 'anon.login') {
            Auth.targetState = null;
        }
        if (!Auth.isAuthorized(toState.data.access)) {
            Auth.targetState = toState.name;
            Auth.targetStateParams = toParams;
            $state.go('anon.login');
        }
    });
}]);