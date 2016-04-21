'use strict';

var yaiaCustomers = angular.module('yaia.customers', ['ui.router', 'restangular']);

yaiaCustomers.config(['$stateProvider', '$urlRouterProvider', function ($stateProvider, $urlRouterProvider) {
  $stateProvider
    .state('user.customers', {
        url: '/customers/:id',
        templateUrl: function ($stateParams) { return 'static/views/partials/' + ($stateParams.id ? 'customer.html' : 'customers.html'); },
        controllerProvider: function ($stateParams) { return $stateParams.id ? 'CustomerCtrl' : 'CustomersCtrl'; },
        resolve: { $title: function() { return 'Customers'; }}
    });
}]);

yaiaCustomers.factory('Customers', ['Restangular', function (Restangular) {
    return Restangular.service('customers');
}]);

yaiaCustomers.controller('CustomersCtrl', ['$scope', 'Customers', function($scope, Customers) {
    Customers.getList().then(
        function(data) {
            $scope.customers = data;
        }
    );
}]);

yaiaCustomers.controller('CustomerCtrl', ['$scope', '$state', '$stateParams', 'Customers', function($scope, $state, $stateParams, Customers) {
    $scope.id = $stateParams.id;
    if ($scope.id == 'new') {
        $scope.title = 'New Customer';
        $scope.customer = {};
        $scope.save = function() {
            Customers.post($scope.customer).then(
                function(data) {
                    $state.go('user.customers', {id: data.id});
                },
                function(resp) {
                    alert("ERROR");
                }
            );
        };
    } else {
        $scope.title = 'Edit Customer';
        $scope.remove = function() {
            $scope.customer.remove().then(
                function(data) {
                    $state.go('user.customers', {id: null});
                },
                function(resp) {
                    alert("ERROR");
                }
            );
        };
        $scope.save = function() {
            $scope.customer.put().then(
                function(data) {
                    alert("Saved");
                },
                function(resp) {
                    alert("ERROR");
                }
            );
        };
        Customers.one($scope.id).get().then(
            function(data) {
                $scope.customer = data;
            }
        );
    }
}]);
