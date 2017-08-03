import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule } from '@angular/forms';

import { MaterialModule } from '@angular/material';

import { UserAuthComponent } from 'app/comp/user_auth/user_auth.component';

const Routes: Routes = [
    { path: '', component: UserAuthComponent },
]

@NgModule({
    imports: [
        CommonModule,
        MaterialModule,
        FormsModule,
        RouterModule.forChild(Routes)
    ],
    declarations: [UserAuthComponent]
})
export class UserAuthModule { }
