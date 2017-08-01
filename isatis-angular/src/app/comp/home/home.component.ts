import { Component, Input, OnChanges, AfterContentChecked, AfterViewInit, ViewChild, AfterContentInit } from '@angular/core';
import { MarkdownService } from 'angular2-markdown';
import { Scrollor } from 'app/service/scrollor.service';

import {
    trigger,
    state,
    style,
    animate,
    transition
} from '@angular/animations';

@Component({
    selector: 'isatis-home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnChanges, AfterViewInit, AfterContentInit {
    public selectTitle = '# Markdown content data \n\
# Markdown content data \n\
# Markdown content data \n\
# Markdown content data \n\
# Markdown content data \n\
# Markdown content data \n\
# Markdown content data \n\
# Markdown content data \n\
# Markdown content data \n\
# Markdown content data \n\
# Markdown content data \n\
# Markdown content data \n\
# Markdown content data \n\
# Markdown content data \n\
# Markdown content data';
    public min_rows = 5;
    public max_rows = 20;
    public dynamic_height = true;
    public tab_position = 'bellow';
    public anchor_tip = { name: 'top' };
    public element = document.querySelector('#ccc');
    @ViewChild('duInput') du_input;
    @ViewChild('duOutput') du_output;

    @Input() title: String;
    constructor(
        private _markdown: MarkdownService,
        private _scrollor: Scrollor
    ) { }

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

    ngAfterViewInit() {

        // setTimeout(() => {
        //     console.log(this.du_input);
        //     console.log(this.du_output);
        //     console.log(this.du_input._viewContainerRef.offsetHeight);
        //     console.log(this.du_output.nativeElement.offsetHeight);
        // }, 0);
    }

    ngAfterContentInit() {

        setTimeout(() => {
            console.log(this.du_input);
            console.log(this.du_output);
        }, 0);


    }

    scroll_top() {
        this.element = document.querySelector('#ccc');
        this._scrollor.scroll_top(this.element);
    }

    scroll_bottom() {
        this.element = document.querySelector('#ccc');
        this._scrollor.scroll_bottom(this.element);
    }

    figure_pos() {
        this.element = document.querySelector('#ccc');
        this._scrollor.figure_pos(this.element);
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
