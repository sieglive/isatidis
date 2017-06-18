import { Component, Input } from '@angular/core';

@Component({
    selector: 'home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.scss']
})
export class HomeComponent {
    @Input() title: String;
    selectTitle = this.title;

    onSelect(title: String): void {
        this.selectTitle = this.title;
    }

    update_title_on_key(event: any, title: String) {
        if (event.key == "Enter") {
            this.selectTitle = title;
        }
    }

    goBack(title: String): void {
        this.selectTitle = title;
    }
}
