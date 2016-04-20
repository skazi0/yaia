'use strict';

var yaiaInvoices = angular.module('yaia.invoices', ['ui.router', 'restangular', 'ngTable']);

yaiaInvoices.config(['$stateProvider', '$urlRouterProvider', function ($stateProvider, $urlRouterProvider) {
  $stateProvider
    .state('user.invoices', {url: '/invoices', templateUrl: 'static/views/partials/invoices.html', controller: 'InvoicesCtrl', resolve: { $title: function() { return 'Invoices'; }}});
}]);

yaiaInvoices.controller('InvoicesCtrl', ['$scope', 'Restangular', 'NgTableParams', function($scope, Restangular, NgTableParams) {
    $scope.tableParams = new NgTableParams(
        {
            count: 10,
        },
        {
            counts: [10, 20, 50, 100],
            getData: function(params) {
                var urlparams = params.url();
                // workaround param syntax not supported by reqparse
                var sortingobj = params.sorting();
                var sortingfields = [];
                for (var key in sortingobj) {
                    sortingfields.push(key + ':' + sortingobj[key]);
                }
                if (sortingfields.length > 0) {
                    urlparams.sorting = sortingfields.join('|');
                }
                return Restangular.one('invoices').get(urlparams).then(
                    function(data) {
                        params.total(data.totalItemCount);
                        return data.items;
                    }
                );
            },
        }
    );
}]);
