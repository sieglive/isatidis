import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SubaboutComponent } from './subabout.component';

describe('SubaboutComponent', () => {
  let component: SubaboutComponent;
  let fixture: ComponentFixture<SubaboutComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SubaboutComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SubaboutComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
