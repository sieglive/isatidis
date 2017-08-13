import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpHeaders, } from '@angular/common/http';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/catch';

@Injectable()
export class IsatisHttp {

    constructor(private http: HttpClient) { }

    wrap_params(params: object) {
        let http_params = new HttpParams();
        for (const key of Object.keys(params)) {
            http_params = http_params.append(key, params[key]);
        }
        return http_params
    }

    wrap_headers(headers: object) {
        let http_headers = new HttpHeaders();
        for (const key of Object.keys(headers)) {
            http_headers = http_headers.append(key, headers[key]);
        }
        return http_headers
    }
}
