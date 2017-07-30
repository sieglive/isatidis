import { Component } from '@angular/core';

@Component({
    selector: 'isatis-bulletin',
    templateUrl: './bulletin.component.html',
    styleUrls: ['./bulletin.component.scss']
})
export class BulletinComponent {
    public tip_list = [
        { title: 'this is acticle A', content: 'this is acticle A' },
        { title: 'this is acticle B', content: 'this is acticle B' },
        { title: 'this is acticle C', content: 'this is acticle C' },
        { title: 'this is acticle D', content: 'this is acticle D' },
        { title: 'this is acticle E', content: 'this is acticle E' },
        { title: 'this is acticle F', content: 'this is acticle F' },
        { title: 'this is acticle G', content: 'this is acticle G' },
    ];

    tipListEmpty() {
    }

    addCard() {

    }
}
