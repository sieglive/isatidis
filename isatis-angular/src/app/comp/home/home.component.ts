import { Component, Input, OnChanges, AfterContentChecked } from '@angular/core';
import { MarkdownService } from 'angular2-markdown';

@Component({
    selector: 'isatis-home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnChanges, AfterContentChecked {
    public selectTitle = '# Markdown content data';
    @Input() title: String;
    constructor(private _markdown: MarkdownService) { }
    // this.selectTitle = this.title;

    // onSelect(title: String): void {
    //     selectTitle = this.title;
    // }

    ngOnChanges(changes: any) {
        console.log(changes);
        const a = this._markdown.compile(this.selectTitle);
        console.log(a);
        // this._markdown.renderer.blockquote = (quote: string) => {
        //     return `<blockquote class="king-quote">${quote}</blockquote>`;
        // }
    }
    ngAfterContentChecked() {
        // const a = this._markdown.compile(this.selectTitle);
        // console.log(a);
    }

    // update_title_on_key(event: any, title: String) {
    //     if (event.key === 'Enter') {
    //         this.selectTitle = title;
    //     }
    // }

    // goBack(title: String): void {
    //     this.selectTitle = title;
    // }
}
