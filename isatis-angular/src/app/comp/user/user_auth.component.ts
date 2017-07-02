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
    private user_time: number;

    constructor(private _http: IsatisHttp) { }

    fetch() {
    }

    signIn() {
        this._http.get(
            '/middle/account/login',
            { email: this.user_email, password: this.user_password },
            res => { const body = res.json(); return body },
            res => { this.user_time = res.time });
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
