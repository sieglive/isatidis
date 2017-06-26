import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class BackgroundService {
  private displayBackground: BehaviorSubject<boolean> = new BehaviorSubject(false);
  constructor() { }
  get getBackground(): Observable<boolean> {
    return this.displayBackground;
  }
  set setBackground(value: boolean) {
    this.displayBackground.next(value);
  }
}
