import { Injectable } from '@angular/core';

@Injectable()
export class Scrollor {
    public element = document.querySelector('#ccc');

    scroll_top() {
        if (this.element) {
            let sss = this.element.scrollTop;
            const delta = sss / 15;
            if (sss > 0) {
                const ccc = setInterval(() => {
                    sss -= delta;
                    this.element.scrollTop = sss;
                    if (sss <= 0) {
                        clearInterval(ccc)
                    }
                }, 5)
            }
        }
    }

    scroll_bottom() {
        if (this.element) {
            const total = this.element.scrollHeight - this.element.clientHeight;
            let sss = this.element.scrollTop;
            const delta = (total - sss) / 15;
            if (sss < total) {
                const ccc = setInterval(() => {
                    sss += delta;
                    this.element.scrollTop = sss;
                    if (sss >= total) {
                        clearInterval(ccc)
                    }
                }, 5)
            }
        }
    }

    figure_pos() {
        if (this.element) {
            console.log('scrollheight', this.element.scrollHeight);
            console.log('clientheight', this.element.clientHeight);
            console.log('scrolltop', this.element.scrollTop);

            // element.scrollIntoView(true);
        }
        return this.element;
    }


}
