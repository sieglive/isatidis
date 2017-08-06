import { Component } from '@angular/core';

@Component({
    selector: 'isatis-bulletin',
    templateUrl: './bulletin.component.html',
    styleUrls: ['./bulletin.component.scss']
})
export class BulletinComponent {
    public tip_list = [
        { title: 'this is acticle A', content: 'this is acticle A', id: 'A' },
        { title: 'this is acticle B', content: 'this is acticle B', id: 'B' },
        { title: 'this is acticle C', content: 'this is acticle C', id: 'C' },
        { title: 'this is acticle D', content: 'this is acticle D', id: 'D' },
        { title: 'this is acticle E', content: 'this is acticle E', id: 'E' },
        { title: 'this is acticle F', content: 'this is acticle F', id: 'F' },
        { title: 'this is acticle G', content: 'this is acticle G', id: 'G' },
    ];
    tipListEmpty() {
    }

    addCard() {

    }
}
