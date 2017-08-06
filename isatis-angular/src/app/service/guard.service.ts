import { Injectable } from '@angular/core';
import {
    CanActivate, Router,
    ActivatedRouteSnapshot,
    RouterStateSnapshot,
    CanActivateChild,
    NavigationExtras,
    CanLoad, Route
} from '@angular/router';
import { AuthService } from './auth.service';

@Injectable()
export class AuthGuard implements CanActivate, CanActivateChild, CanLoad {
    constructor(private authService: AuthService, private router: Router) { }

    canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
        // const url: string = state.url;

        // return this.checkLogin(url);

        const navigationExtras: NavigationExtras = {
            queryParams: { 'session_id': 123456789 },
            fragment: 'anchor'
        };

        console.log(route, state);
        this.router.navigate(['/auth'], navigationExtras);
        return false;
    }

    canActivateChild(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
        // return this.canActivate(route, state);
        console.log('activechild');
        return false;
    }

    canLoad(route: Route): boolean {
        // const url = `/${route.path}`;

        // return this.checkLogin(url);
        console.log(route);
        return false;
    }

    checkLogin(url: string): boolean {
        if (this.authService.isLoggedIn) { return true; }

        // Store the attempted URL for redirecting
        this.authService.redirectUrl = url;

        // Create a dummy session id
        const sessionId = 123456789;

        // Set our navigation extras object
        // that contains our global query params and fragment
        const navigationExtras: NavigationExtras = {
            queryParams: { 'session_id': sessionId },
            fragment: 'anchor'
        };

        // Navigate to the login page with extras
        this.router.navigate(['/login'], navigationExtras);
        return false;
    }
}

@Injectable()
export class ExAuthGuard implements CanActivate, CanActivateChild, CanLoad {
    constructor(private authService: AuthService, private router: Router) { }

    canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
        console.log(route, state);
        return true;
    }

    canActivateChild(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
        console.log('activechild');
        return true;
    }

    canLoad(route: Route): boolean {
        console.log(route);
        return true;
    }

    checkLogin(url: string): boolean {
        return true;
    }

}
