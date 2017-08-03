import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule } from '@angular/forms';

import { MaterialModule } from '@angular/material';

import { ProfileComponent } from 'app/comp/profile/profile.component';

const Routes: Routes = [
    { path: '', component: ProfileComponent },
]

@NgModule({
    imports: [
        CommonModule,
        MaterialModule,
        FormsModule,
        RouterModule.forChild(Routes)
    ],
    declarations: [ProfileComponent]
})
export class ProfileModule { }
