import { Component } from '@angular/core';

import { IsatisHttp } from 'app/service/isatis_http.service';

@Component({
    selector: 'isatis-user-auth',
    templateUrl: './user_auth.component.html',
    styleUrls: ['./user_auth.component.scss']
})
export class UserAuthComponent {
    public user_email = '';
    public user_password = '';
    public user_account = '';
    public user_nick = '';
    public result: any;
    public user_time: number;

    constructor(private _http: IsatisHttp) { }

    fetch() {
    }

    signIn() {
        const result = this._http.post(
            '/back/account/auth',
            {
                email: this.user_email,
                user_pass: this.user_password
            }
        );
        result.subscribe(res => { this.user_time = res.json().time; });
    }

    signUp() {
        const result = this._http.put(
            '/back/account/auth',
            {
                email: this.user_email,
                user_pass: this.user_password,
                nick_name: this.user_nick,
                user_name: this.user_account
            }
        );
        console.log(this.user_nick);
        result.subscribe(res => { this.user_time = res.json().time; });
    }
}
