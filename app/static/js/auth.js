'use strict';

var yaiaAuth = angular.module('yaia.auth', ['restangular']);

yaiaAuth.factory('Auth', ['Restangular', '$rootScope', function (Restangular, $rootScope) {
    var user = null;

    function notifyAuthChange() {
        $rootScope.$broadcast('authChanged', user);
        console.log('sent authChanged');
    }

    function updateAuthInfo() {
        Restangular.one('sessions').get().then(
            function(sessions) {
                user = sessions[0];
                notifyAuthChange();
            }
        );
    }

    function clearAuthInfo() {
        user = null;
        notifyAuthChange();
    }


    function currentUser() {
        return user;
    }

    function isAuthorized(level) {
        if (level == 'anon')
            return true;

        return currentUser() != null && currentUser().authenticated;
    }

    function login(username, password, remember) {
        var session = {login: username, password: password, remember: remember};
        return Restangular.all('sessions').post(session).then(
            function(data) {
// skz: for some reason this doesn't get recognized in $on
//                user = data;
//                notifyAuthChange();
                updateAuthInfo();
                return data;
            }
        );
    }

    function logout() {
        return Restangular.all('sessions').remove().then(clearAuthInfo, clearAuthInfo);
    }

    return { 
        isAuthorized: isAuthorized,
        login: login,
        logout: logout,
        currentUser: currentUser,
        refresh: updateAuthInfo,
    };
}]);
