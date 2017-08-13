import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { MaterialModule } from '@angular/material';

import { UserAuthComponent } from './user_auth.component';

const Routes: Routes = [
    { path: '', component: UserAuthComponent },
]

@NgModule({
    imports: [
        CommonModule,
        MaterialModule,
        FormsModule,
        HttpClientModule,
        RouterModule.forChild(Routes)
    ],
    declarations: [UserAuthComponent]
})
export class UserAuthModule { }
