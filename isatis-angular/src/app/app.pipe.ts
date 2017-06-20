import { Pipe, PipeTransform } from '@angular/core';

@Pipe({name: 'convert'})
export class ConvertFormat implements PipeTransform {
    transform(mytext: string): string {
        return mytext.replace('\n', '<br/>');
    }
}
