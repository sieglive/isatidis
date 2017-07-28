import { Component } from '@angular/core';

@Component({
    selector: 'isatis-bulletin',
    templateUrl: './bulletin.component.html',
    styleUrls: ['./bulletin.component.scss']
})
export class BulletinComponent {
    public tip_list = [1, 2, 3, 4, 5, 6, 7, 8, 9];

    tipListEmpty() {
    }

    addCard() {

    }
}
