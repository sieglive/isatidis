import { Component, OnInit, Directive, ViewChild } from '@angular/core';

import { Scrollor } from 'app/service/scrollor.service';


@Component({
    selector: 'isatis-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})

export class AppComponent implements OnInit {

    private disabled_background = false;
    public element: any

    constructor(private _scrollor: Scrollor) {
    }

    ngOnInit() {
        this.element = document.querySelector('#ccc');
        console.log(this.element);
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
        this._scrollor.figure_scroll_top(this.element);
    }
    // change_bg() {
    //     if (this.toggle) {
    //         this.winRef.nativeWindow.pJSDom = [];
    //         this.winRef.nativeWindow.particlesJS.load('particles-js', 'assets/particles.json', function () {
    //             console.log('callback - particles.js config loaded');
    //         });
    //     } else {
    //         this.winRef.nativeWindow.pJSDom[0].pJS.interactivity.events.onclick.enable = false;
    //         this.winRef.nativeWindow.pJSDom[0].pJS.interactivity.events.onhover.enable = false;
    //         this.winRef.nativeWindow.pJSDom[0].pJS.particles.array = [];
    //         this.winRef.nativeWindow.pJSDom[0].pJS.particles.move.enable = false;
    //     }
    // }

    // clean_bg() {
    //     this.winRef.nativeWindow.pJSDom[0].pJS.particles.array = [];
    // }

}
