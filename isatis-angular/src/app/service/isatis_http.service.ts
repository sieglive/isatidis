import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/catch';

@Injectable()
export class IsatisHttp {

    constructor(private http: Http) { }

    get(url: string, params: object): Observable<Response> {
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
        return this.http.get(requestUrl).catch(this.handleError);
    }

    post(url: string, params: object): Observable<Response> {
        return this.http.post(url, params).catch(this.handleError);
    }

    put(url: string, params: object): Observable<Response> {
        return this.http.put(url, params).catch(this.handleError);
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
