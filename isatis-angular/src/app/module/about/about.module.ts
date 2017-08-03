import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule } from '@angular/forms';

import { MaterialModule } from '@angular/material';

import { AboutComponent } from './about.component';

const aboutRoutes: Routes = [
    { path: '', component: AboutComponent },
]

@NgModule({
    imports: [
        CommonModule,
        MaterialModule,
        FormsModule,
        RouterModule.forChild(aboutRoutes)
    ],
    declarations: [
        AboutComponent
    ]
})
export class AboutModule { }
