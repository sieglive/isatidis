import { Component } from '@angular/core';
import { MdSnackBar } from '@angular/material';
import { Router } from '@angular/router';

import { IsatisHttp } from 'app/service/isatis_http.service';
import { HttpClient } from '@angular/common/http';
@Component({
    selector: 'isatis-user-auth',
    templateUrl: './user_auth.component.html',
    styleUrls: ['./user_auth.component.scss']
})
export class UserAuthComponent {
    public sign_up_data = {
        email: '',
        password: '',
        confirm_pass: '',
        nickname: ''
    }

    public sign_in_data = {
        email: '',
        password: '',
    }

    public form_data = {
        email_tooltip: 'Enter Your Email',
        pass_tooltip: `Password should contain 6-24 characters.
                Charaters include number, letter, and most of the other characters on keyboard.`,
        nick_tooltip: 'Nickname should contain 6-24 characters. Accept most chinese word and English word, include "-" and "_"',
        confirm_tooltip: 'Confirm Your Password'
    }

    public result: any;
    public user_time: number;
    public pattern = {
        email: /^([\w-]+)@([\w-]+)(\.([\w-]+))+$/,
        password: /^[0-9A-Za-z`~!@#$%^&*()_+\-=\{\}\[\]:;"'<>,.\\|?/ ]{6,24}$/,
        nickname: /^[\w\-\u4e00-\u9fa5]{1,24}$/,
    }


    position = 'right';

    constructor(
        private _http_util: IsatisHttp,
        private _http: HttpClient,
        private _router: Router,
        public snack_bar: MdSnackBar
    ) { }

    fetch() {
    }

    raiseSnackBar(message: string, action_name: string, action) {
        const snack_ref = this.snack_bar.open(
            message,
            action_name,
            {
                duration: 2000,
            }
        );
        snack_ref.onAction().subscribe(action);
    }

    signIn() {
        this.sign_in_data.email = this.sign_in_data.email.trim();
        let message = '';
        let not_regular = false;
        if (!this.sign_in_data.email.match(this.pattern.email)) {
            message = 'Invalid Email.';
            not_regular = true;
        } else if (!this.sign_in_data.password.match(this.pattern.password)) {
            message = 'Invalid Password.';
            not_regular = true;
        }
        if (not_regular) {
            this.raiseSnackBar(message, 'OK', () => {
                console.log('The snack-bar action was triggered!');
            });
            return false;
        }
        const result = this._http.post(
            '/middle/account/signin',
            {
                email: this.sign_in_data.email,
                password: this.sign_in_data.password
            });
        result.subscribe(
            data => {
                if (data['result'] === 1) {
                    this._router.navigate(['/home']);
                } else {
                    this.raiseSnackBar(data['msg'], 'OK', () => {
                        console.log('Got it.');
                    });
                    console.log(data);
                    return false;
                }
            });
    }


    signUp() {
        this.sign_up_data.email = this.sign_up_data.email.trim();
        let message = '';
        let not_regular = false;
        if (!this.sign_up_data.nickname.match(this.pattern.nickname)) {
            message = 'Invalid Nickname.';
            not_regular = true;
        } else if (!this.sign_up_data.email.match(this.pattern.email)) {
            message = 'Invalid Email.';
            not_regular = true;
        } else if (!this.sign_up_data.password.match(this.pattern.password)) {
            message = 'Invalid Password.';
            not_regular = true;
        } else if (this.sign_up_data.password !== this.sign_up_data.confirm_pass) {
            message = 'Password is inconsistent';
            not_regular = true;
        }
        if (not_regular) {
            const snack_ref = this.snack_bar.open(
                message,
                '',
                {
                    duration: 2000,
                }
            );

            snack_ref.onAction().subscribe(() => {
                console.log('The snack-bar action was triggered!');
            });
            return false;
        }
        const result = this._http.post(
            '/middle/account/signup',
            {
                nickname: this.sign_up_data.nickname,
                email: this.sign_up_data.email,
                password: this.sign_up_data.password
            });
        result.subscribe(
            data => { console.log('success', data); },
            err => { console.log('error', err); }
        );
    }
}
