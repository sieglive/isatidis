import {
    Component,
    Directive,
    ElementRef,
    Input,
    Output,
    EventEmitter,
    ViewChild,
    OnInit,
    OnChanges,
    OnDestroy,
    AfterContentChecked,
    AfterViewChecked,
    AfterViewInit,
    AfterContentInit
} from '@angular/core';
import { MarkdownService } from 'angular2-markdown';
import { Scrollor } from 'app/service/scrollor.service';
import { HighlightJsService } from 'angular2-highlight-js';

import {
    trigger,
    state,
    style,
    animate,
    transition
} from '@angular/animations';

@Directive({
    selector: '[isatisMd]'
})
export class MarkdownDirective implements OnChanges {
    @Input() set data(value: string) {
    }

    constructor(
        private _markdown: MarkdownService,
        public _scrollor: Scrollor,
        private el: ElementRef,
        private _hljsservice: HighlightJsService
    ) { }
    ngOnChanges(changes: any) {
        console.log(changes);
        const element_list = this.el.nativeElement.querySelectorAll('pre code');
        for (let i = 0; i < element_list.length; i++) {
            this._hljsservice.highlight(element_list[i]);
        }
    }
}

@Component({
    selector: 'isatis-home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit, OnChanges, AfterContentChecked, AfterViewChecked, AfterViewInit, AfterContentInit {
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
    public element: any;
    public tab1: any;
    public tab_height_1: number;
    public tab_height_2: number;
    public tab2: any;
    public tab_select = 0;
    public show_scroll: boolean;
    @ViewChild('duInput') du_input;
    @ViewChild('duOutput') du_output;

    @Input() title: String;
    constructor(
        private _markdown: MarkdownService,
        public _scrollor: Scrollor,
        private el: ElementRef,
        private _hljsservice: HighlightJsService
    ) { }

    ngOnInit() {
        this.element = document.querySelector('#ccc');

    }
    ngOnChanges(changes: any) {
        // console.log('changes', changes);
    }
    ngAfterViewInit() {
        // this.element = this.el.nativeElement.querySelector('pre');
        // if (this.element) {
        //     console.log(this.element);
        //     this._hljsservice.highlight(this.element);
        // }


        // console.log('view', this.element.scrollTop, this.element.scrollHeight);
    }

    ngAfterContentInit() {
        // console.log('content', this.element.scrollTop, this.element.scrollHeight);

    }

    ngAfterViewChecked() {
        // const tab1 = document.querySelector('#tab1');
        // const tab2 = document.querySelector('#tab2');
        // if (tab1) {
        //     this.tab_height_1 = tab1.clientHeight;
        // } else if (tab2) {
        //     this.tab_height_2 = tab2.clientHeight;
        // }
        // console.log('viewcheck', this.element.scrollTop, this.element.scrollHeight, this.tab1.clientHeight);
    }

    ngAfterContentChecked() {
        // const tab1 = document.querySelector('#tab1');
        // const tab2 = document.querySelector('#tab2');
        // if (tab1) {
        //     this.tab_height_1 = tab1.clientHeight;
        // } else if (tab2) {
        //     this.tab_height_2 = tab2.clientHeight;
        // }
        // console.log(this.tab_height_1, this.tab_height_2);
        // console.log('contentcheck', this.element.scrollTop, this.element.scrollHeight, this.tab2.clientHeight);
    }

    scroll_top() {
        this._scrollor.scroll_top(this.element);
    }

    scroll_bottom() {
        this._scrollor.scroll_bottom(this.element);
    }

    figure_pos() {
        this._scrollor.figure_pos(this.element);
    }

    figure_scroll_top() {
        if (this.element.scrollTop > 100) {
            this.show_scroll = true;
            return true;
        } else {
            this.show_scroll = false;
            return false;
        }
    }

    select1() {
        this.tab_select = 0;
    }

    select2() {
        this.tab_select = 1;
    }
    // update_title_on_key(event: any, title: String) {
    //     if (event.key === 'Enter') {
    //         this.selectTitle = title;
    //     }
    // }

    // goBack(title: String): void {
    //     this.selectTitle = title;
    // }
    select_change(event) {
        // console.log(this.tab_height_1, this.tab_height_2);
        this.tab_select = event;
        // const element_list = this.el.nativeElement.querySelectorAll('pre code');
        // for (let i = 0; i < element_list.length; i++) {
        //     this._hljsservice.highlight(element_list[i]);
        // }
    }
}
