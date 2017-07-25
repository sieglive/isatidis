import { Component, OnChanges, DoCheck } from '@angular/core';

@Component({
    selector: 'isatis-profile',
    templateUrl: './profile.component.html',
    styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnChanges, DoCheck {
    public user_email = '';
    public user_account = '';
    public user_name = '';
    public user_nick = '';
    public properties = [
        { name: 'Nick Name', value: this.user_nick },
        { name: 'Account', value: this.user_account },
        { name: 'True Name', value: this.user_name },
        { name: 'Email', value: this.user_email }
    ]

    ngOnChanges(change) {
        console.log(change);
        console.log(this.user_nick, this.user_account, this.user_name, this.user_email);
    }


    ngDoCheck() {
        console.log(this.properties);
    }

    test() {
        console.log('cancle');
    }
}
