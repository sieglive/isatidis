import { Component, OnInit, Directive, ViewChild, AfterViewInit } from '@angular/core';
// import { WindowRef } from 'app/service/window.service';
// import { BackgroundService } from 'app/background.service';


@Component({
    selector: 'isatis-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})

export class AppComponent implements OnInit, AfterViewInit {

    private disabled_background = false;
    // private toggle = false;
    constructor() { }

    ngOnInit() {
        // if (this.toggle) {
        //     this.winRef.nativeWindow.particlesJS.load('particles-js', 'assets/particles.json', function () {
        //         console.log('callback - particles.js config loaded');
        //     });
        // }
    }

    ngAfterViewInit() {
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
