import { Component } from '@angular/core';

import { IsatisHttp } from 'app/service/isatis_http.service';

@Component({
    selector: 'isatis-user-auth',
    templateUrl: './user_auth.component.html',
    styleUrls: ['./user_auth.component.scss']
})
export class UserAuthComponent {
    private user_email: string;
    private user_password: string;
    private resObject: object;
    private res: object;

    constructor(private _http: IsatisHttp) { }

    fetch() {
    }

    signIn() {
        this._http.res = {
            url: '/middle/account/login',
            params: { email: this.user_email + '1', password: this.user_password }
        };
    }
    signIn2() {
        this._http.res = {
            url: '/middle/account/login',
            params: { email: this.user_email + '2', password: this.user_password }
        };
    }
    signIn3() {
        this.resObject = this._http.res;
        console.log('component1', this.resObject);
    }
    signIn4() {
        this.resObject = this._http.res;
        console.log('component2', this.resObject);
    }

    // signUp() {
    //     this._http.res = {
    //         url: '/middle/account/login',
    //         params: { email: this.user_email, password: this.user_password },
    //         callback: res => {
    //             const body = res.json();
    //             return body;
    //         }
    //     }
    //     console.log(this._http.res);

    // }
}
