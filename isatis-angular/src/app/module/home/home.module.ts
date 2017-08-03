import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { FormsModule } from '@angular/forms';

import { MaterialModule } from '@angular/material';
import { MarkdownModule } from 'angular2-markdown';

import { HomeComponent, MarkdownDirective } from './home.component'

const Routes: Routes = [
    { path: '', component: HomeComponent },
]

@NgModule({
    imports: [
        CommonModule,
        MaterialModule,
        FormsModule,
        MarkdownModule.forRoot(),
        RouterModule.forChild(Routes)
    ],
    declarations: [
        HomeComponent,
        MarkdownDirective
    ]
})
export class HomeModule { }
