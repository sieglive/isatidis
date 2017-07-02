import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/map';

@Injectable()
export class IsatisHttp {

    constructor(private http: Http) { }

    get(url: string, params: object, extra: any, callback: any) {
        let requestUrl = url;

        // 拼接URL
        if (params) {
            requestUrl += '?';
            for (const key of Object.keys(params)) {
                requestUrl += (key + '=' + params[key] + '&');
            }
        }

        // 去掉最后一个 &
        requestUrl = requestUrl.substring(0, requestUrl.length - 1);
        const res = this.http.get(requestUrl).map(extra).catch(this.handleError)
        return res.subscribe(callback);
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
