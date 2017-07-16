import { Component, OnChanges, DoCheck } from '@angular/core';

@Component({
    selector: 'isatis-profile',
    templateUrl: './profile.component.html',
    styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnChanges, DoCheck {
    public user_email = '';
    public user_pass = '';
    public user_name = '';
    public user_nick = '';
    public properties = [
        { name: 'user_nick', value: this.user_nick },
        { name: 'user_pass', value: this.user_pass },
        { name: 'user_name', value: this.user_name },
        { name: 'user_email', value: this.user_email }
    ]

    ngOnChanges(change) {
        console.log(change);
        console.log(this.user_nick, this.user_pass, this.user_name, this.user_email);
    }


    ngDoCheck() {
        console.log(this.properties);
    }
}
