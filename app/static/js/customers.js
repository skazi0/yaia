'use strict';

var yaiaCustomers = angular.module('yaia.customers', ['ui.router', 'restangular']);

yaiaCustomers.config(['$stateProvider', '$urlRouterProvider', function ($stateProvider, $urlRouterProvider) {
  $stateProvider
    .state('user.customers', {
        url: '/customers/:id',
        templateUrl: function ($stateParams) { return 'static/views/partials/' + ($stateParams.id ? 'customer.html' : 'customers.html'); },
        controllerProvider: function ($stateParams) { return $stateParams.id ? 'CustomerCtrl' : 'CustomersCtrl'; },
    });
}]);

yaiaCustomers.controller('CustomersCtrl', ['$scope', 'Restangular', function($scope, Restangular) {
    Restangular.all('customers').getList().then(
        function(data) {
            $scope.customers = data;
        }
    );
}]);

yaiaCustomers.controller('CustomerCtrl', ['$scope', '$stateParams', 'Restangular', function($scope, $stateParams, Restangular) {
    $scope.customer = $stateParams.id;
}]);
