import { Injectable } from '@angular/core';

@Injectable()
export class Scrollor {

    scroll_top(el) {
        if (el) {
            let sss = el.scrollTop;
            const delta = sss / 15;
            if (sss > 0) {
                const ccc = setInterval(() => {
                    sss -= delta;
                    el.scrollTop = sss;
                    if (sss <= 0) {
                        clearInterval(ccc);
                    }
                }, 5);
            }
        }
    }

    scroll_bottom(el) {
        if (el) {
            const total = el.scrollHeight - el.clientHeight;
            let sss = el.scrollTop;
            const delta = (total - sss) / 15;
            if (sss < total) {
                const ccc = setInterval(() => {
                    sss += delta;
                    el.scrollTop = sss;
                    if (sss >= total) {
                        clearInterval(ccc);
                    }
                }, 5);
            }
        }
    }

    figure_pos(el) {
        if (el) {
            console.log('scrollheight', el.scrollHeight);
            console.log('clientheight', el.clientHeight);
            console.log('scrolltop', el.scrollTop);

            // element.scrollIntoView(true);
        }
        return el;
    }


}
