import { Component, OnInit } from '@angular/core';
import { WindowRef } from 'app/service/window.service';

@Component({
    selector: 'isatis-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
    constructor(private winRef: WindowRef) { }
    ngOnInit() {

        this.winRef.nativeWindow.particlesJS.load('particles-js', 'assets/particles.json', function () {
            console.log('callback - particles.js config loaded');
        });
    }
    clean_bg() {
        this.winRef.nativeWindow.pJSDom[0].pJS.particles.array = [];
    }
}
