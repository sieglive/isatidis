import { Component } from '@angular/core';

import { Http, Response } from '@angular/http';

import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/map';


@Component({
    selector: 'isatis-user-auth',
    templateUrl: './user_auth.component.html',
    styleUrls: ['./user_auth.component.scss']
})
export class UserAuthComponent {
    private heroesUrl = '/middle/account/login';  // URL to web API

    constructor(private http: Http) { }

    get_res() {
        this.getRes().subscribe(res => { console.log(res); });
    }

    getRes(): Observable<Object> {
        console.log('test');
        return this.http.post(this.heroesUrl, { email: "314624180@qq.com", password: "111111" })
            .map(this.extractData).catch(this.handleError);
    }

    private extractData(res: Response) {
        console.log(res);
        let body = res.json();
        return body.email || {};
    }

    private handleError(error: Response | any) {
        // In a real world app, you might use a remote logging infrastructure
        let errMsg: string;
        if (error instanceof Response) {
            const body = error.json() || '';
            const err = body.error || JSON.stringify(body);
            errMsg = `${error.status} - ${error.statusText || ''} ${err}`;
        } else {
            errMsg = error.message ? error.message : error.toString();
        }
        console.error(errMsg);
        return Observable.throw(errMsg);
    }
}
