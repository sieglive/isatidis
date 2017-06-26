import { Pipe, PipeTransform } from '@angular/core';

@Pipe({name: 'convert'})
export class ConvertFormat implements PipeTransform {
    transform(mytext: string): string {
        mytext = mytext.replace('真帅', '真傻逼');
        if (mytext.search(/abc/) !== -1) {
            return 'Hello Django!'
        }
        mytext = mytext.replace(/a/g, 's');
        mytext = mytext.replace(/b/g, 't');
        mytext = mytext.replace(/c/g, 'p');
        return mytext
    }
}
