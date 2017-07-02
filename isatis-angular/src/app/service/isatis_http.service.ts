import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/map';

@Injectable()
export class IsatisHttp {
    private _http_res: BehaviorSubject<object> = new BehaviorSubject({});

    constructor(private http: Http) { }

    get res(): any {
        // let backOb: Observable<object> = null;
        let backRes: object = null;
        this._http_res.subscribe(res => backRes = res);
        console.log('backRes', backRes);
        return backRes;
    }

    set res(value: any) {
        const back = this.get(value.url, value.params, res => { const body = res.json(); return body; });
        back.subscribe(res => this._http_res.next(res))
    }

    get(url: string, params: object, callback: any): Observable<Object> {
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

        return this.http.get(requestUrl)
            .map(callback).catch(this.handleError);
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
