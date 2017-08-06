import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule } from '@angular/forms';

import { MaterialModule } from '@angular/material';

import { BulletinComponent } from './bulletin.component';

const Routes: Routes = [
    { path: '', component: BulletinComponent },
]

@NgModule({
    imports: [
        CommonModule,
        MaterialModule,
        FormsModule,
        RouterModule.forChild(Routes)
    ],
    declarations: [
        BulletinComponent
    ]
})
export class BulletinModule { }
